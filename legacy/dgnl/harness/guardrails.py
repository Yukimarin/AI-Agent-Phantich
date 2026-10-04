import sys
import os

class Guardrails:
    @staticmethod
    def check_stdout_limit(content, limit_chars=10000):
        """
        Ensures that large output is not printed directly to stdout,
        which would bloat the token usage.
        """
        if len(content) > limit_chars:
            print(f"[Warning] Output is too large ({len(content)} chars). Truncating to prevent token bloat.")
            return content[:limit_chars] + "\n... [TRUNCATED FOR TOKEN OPTIMIZATION]"
        return content

    @staticmethod
    def check_file_size(file_path, max_bytes=50 * 1024 * 1024):
        """
        Checks if file size is within limits to prevent OOM or crash.
        """
        if not os.path.exists(file_path):
            return False
        return os.path.getsize(file_path) <= max_bytes

    @staticmethod
    def log_agent_action(action_name, details):
        """
        Standard logging for observability in Harness Architecture.
        """
        print(f"[Harness Log] Action: {action_name} | Details: {details}")

if __name__ == "__main__":
    # Self-test
    Guardrails.log_agent_action("SelfTest", "Guardrails initialization successful.")
