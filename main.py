import config
import uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG
    )

