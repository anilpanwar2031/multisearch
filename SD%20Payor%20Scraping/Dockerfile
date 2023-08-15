FROM python:latest	
ENV  TZ="America/New_York"
ENV DISPLAY=host.docker.internal:0.0
RUN apt-get -y update
RUN apt-get install -y xvfb
RUN pip install PyVirtualDisplay==3.0
RUN apt-get install -y default-jdk
RUN pip install fitz
RUN pip install pdfplumber
RUN apt-get install -yqq unzip

RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_108.0.5359.98-1_amd64.deb && apt install -y /tmp/chrome.deb && rm /tmp/chrome.deb



RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN chmod +w /usr/local/bin/chromedriver
RUN apt-get -y install vim 
RUN vim /usr/local/bin/chromedriver -c ":%s/cdc_/mani/g" -c "wq"
RUN chmod -w /usr/local/bin/chromedriver

WORKDIR /scraper
COPY . .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python3", "main.py"]