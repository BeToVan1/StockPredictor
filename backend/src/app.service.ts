import { exec } from 'child_process';
import { Injectable } from '@nestjs/common';
import * as finnhub from 'finnhub';
import axios from 'axios';
import * as path from 'path';

@Injectable()
export class PredictService {
  async predict(ticker: string, windowSize = 60, daysAhead = 5): Promise<any> {
    return new Promise((resolve, reject) => {
      const scriptPath = path.join(__dirname, '../../ml-service/inference/predict_next_close.py')
      const command = `python ${scriptPath} ${ticker} ${windowSize} ${daysAhead}`;
      console.log('Running command: ', command);
      exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error(`❌ Python Error: ${stderr}`);
          return reject(`Python execution failed: ${stderr}`);
        }

        try {
          const result = JSON.parse(stdout.trim());
          resolve(result);
        } catch (parseErr) {
          console.error(`❌ JSON Parse Error: ${stdout}`);
          reject(`Failed to parse prediction output: ${stdout}`);
        }
      });
    });
  }
}

@Injectable()
export class NewsService {
  async getCompanyNews(symbol: string, from: string, to: string) {
    const url = `https://finnhub.io/api/v1/company-news?symbol=${symbol}&from=${from}&to=${to}&token=${process.env.FINNHUB_API_KEY}`;
    const { data } = await axios.get(url);
    console.log("HELLO");
    console.log(data);
    return data;
  }
}
