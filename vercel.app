{
    "builds": [{
        "src": "server3/wsgi.py",
        "use": "@vercel/python",
        "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
    }],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "server3/wsgi.py"
        }
    ]
}