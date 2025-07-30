import { exec } from 'child_process';
import { Injectable } from '@nestjs/common';

@Injectable()
export class PredictService {
  async predict(ticker: string, windowSize = 60, daysAhead = 5): Promise<any> {
    return new Promise((resolve, reject) => {
      const command = `python ../ml-service/inference/predict_next_close.py ${ticker} ${windowSize} ${daysAhead}`;
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
