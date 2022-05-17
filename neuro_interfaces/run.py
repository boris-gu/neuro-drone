import uvicorn as uvicorn
import settings

if __name__ == '__main__':
    print("Drone control service is running...")
    uvicorn.run("http_server:app", host='0.0.0.0',
                port=settings.APP_PORT, reload=False, debug=True, workers=1)
