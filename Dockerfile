FROM python

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install -i /usr/local/aws-cli -b /usr/local/bin \
    && rm awscliv2.zip \

WORKDIR /app
COPY requirements.txt .
COPY . .

RUN pip install -r requirements.txt
RUN pip install --no-cache-dir boto3

ENTRYPOINT ["python", "main.py"]