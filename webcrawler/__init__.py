import os

os.environ["THREADS"] = os.getenv("THREADS", "1")
os.environ["LOGGER_LEVEL"] = os.getenv("LOGGER_LEVEL", "debug")
os.environ["LOG_CURL_REQUESTS"] = os.getenv("LOG_CURL_REQUESTS", "1")
os.environ["MYSQL_LOG_QUERIES"] = os.getenv("MYSQL_LOG_QUERIES", "0")
os.environ["ELASTICSEARCH_MONITOR_TAGS"] = os.getenv("ELASTICSEARCH_MONITOR_TAGS", "component:webcrawler")
os.environ["HEADLESS_BROWSER"] = os.getenv("HEADLESS_BROWSER", "0")

os.environ["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
os.environ["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "123123")
os.environ["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "127.0.0.1")
os.environ["MYSQL_PORT"] = os.getenv("MYSQL_PORT", "3309")
os.environ["MYSQL_SCHEME"] = os.getenv("MYSQL_SCHEME", "lifestyle")
os.environ["JSON_LOG_CONSOLE"] = os.getenv("JSON_LOG_CONSOLE", "0")

os.environ["DEBUG_MODE"] = os.getenv("DEBUG_MODE", "1")
