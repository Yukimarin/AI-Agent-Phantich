const https = require('https');

function call_mcp_tool(tool_name, arguments) {
    return new Promise((resolve, reject) => {
        const payload = JSON.stringify({
            jsonrpc: "2.0",
            id: 1,
            method: "tools/call",
            params: {
                name: tool_name,
                arguments: arguments || {}
            }
        });

        const options = {
            hostname: 'pm.rikkei.edu.vn',
            port: 443,
            path: '/api/mcp',
            method: 'POST',
            headers: {
                'Authorization': 'Bearer wl_jtpd1dOgxnUm5n2d7V6dxBT_AZHNrnCK',
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(payload),
                'Accept': 'application/json, text/event-stream'
            },
            rejectUnauthorized: false
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            res.on('end', () => {
                try {
                    const lines = data.split('\n');
                    for (const line of lines) {
                        if (line.startsWith('data:')) {
                            const jsonStr = line.substring(5).trim();
                            const parsed = JSON.parse(jsonStr);
                            resolve(parsed);
                            return;
                        }
                    }
                    resolve(null);
                } catch (e) {
                    reject(e);
                }
            });
        });

        req.on('error', (e) => {
            reject(e);
        });

        req.write(payload);
        req.end();
    });
}

async function run() {
    const dates = ["2026-07-27", "2026-07-28", "2026-07-29", "2026-07-30", "2026-07-31", "2026-08-01"];
    let allDifficulties = [];
    
    for (const d of dates) {
        try {
            const res = await call_mcp_tool("list_daily_reports", { date: d, department: "DT" });
            if (res && res.result && res.result.content && res.result.content.length > 0) {
                const innerStr = res.result.content[0].text || "";
                const innerJson = JSON.parse(innerStr);
                const reports = innerJson.reports || [];
                
                for (const r of reports) {
                    const user = r.user || r.name;
                    let diff = r.difficulties || r.difficulty || r.issue || r.issues || r.note;
                    if (r['khó khăn']) diff = r['khó khăn'];
                    
                    if (diff && typeof diff === 'string' && diff.trim() !== '') {
                        allDifficulties.push({ date: d, user: user, difficulty: diff });
                    } else {
                        // Check keys
                        for (const [k, v] of Object.entries(r)) {
                            if (v && typeof v === 'string' && (k.toLowerCase().includes('khó khăn') || k.toLowerCase().includes('vấn đề') || k.toLowerCase().includes('issue') || k.toLowerCase().includes('difficult'))) {
                                allDifficulties.push({ date: d, user: user, difficulty: `${k}: ${v}` });
                            }
                        }
                    }
                }
            }
        } catch (e) {
            console.error(`Error on date ${d}:`, e);
        }
    }
    
    console.log(JSON.stringify(allDifficulties, null, 2));

    console.log("\n--- SAMPLE REPORT FORMAT ---");
    try {
        const res = await call_mcp_tool("list_daily_reports", { date: "2026-07-27", department: "DT" });
        if (res && res.result && res.result.content && res.result.content.length > 0) {
            const innerStr = res.result.content[0].text || "";
            const innerJson = JSON.parse(innerStr);
            if (innerJson.reports && innerJson.reports.length > 0) {
                console.log(JSON.stringify(innerJson.reports[0], null, 2));
            }
        }
    } catch(e) {}
}

run();
