import uvicorn
import os
import time

uvicorn.run("backend:app", port = 3000, log_level="info")
