## Test Execution

1. Create virtualenv and install requirements:
    ```bash
    $ virtualenv venv 
    $ source venv/bin/activate 
    $ cd test
    $ pip install -r requirements.txt
    ```

2. Run zap
In daemon mode with a specified api key and if you have installed ZAP previously, you can run:
    ```bash
    $ zap.sh -daemon -config api.key=change-me-9203935709
    ```
If you don't have ZAP installed, you can run it using Docker:
    ```bash
    $ docker run -u zap -p 8080:8080 -i owasp/zap2docker-stable zap.sh -daemon -config api.key=change-me-9203935709
    ```

3. Execute test cases
    ```bash
    $ cd test
    $ behave
    ```
