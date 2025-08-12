import { Controller, Get, Query, HttpException, HttpStatus } from '@nestjs/common';
import { PredictService, NewsService } from './app.service';
import * as finnhub from 'finnhub';
import { ConfigService } from '@nestjs/config';

@Controller('predict')
export class PredictController {
  constructor(private readonly predictService: PredictService) {}

  @Get()
  async getPrediction(
    @Query('ticker') ticker: string,
    @Query('windowSize') windowSize: string,
    @Query('daysAhead') daysAhead: string,
  ) {
    const prediction = await this.predictService.predict(
      ticker,
      parseInt('60'),
      parseInt(daysAhead),
    );
    return prediction;
  }
}

@Controller('news')
export class NewsController {
  constructor(private readonly newsService: NewsService) {}

  @Get()
  async getNews(@Query('ticker') ticker: string) {
    if (!ticker) {
      throw new HttpException('Ticker is required', HttpStatus.BAD_REQUEST);
    }

    const today = new Date();
    const fromDate = new Date();
    fromDate.setDate(today.getDate() - 7);

    const fromStr = fromDate.toISOString().split('T')[0];
    const toStr = today.toISOString().split('T')[0];

    try {
      const articles = await this.newsService.getCompanyNews(ticker, fromStr, toStr);
      return { articles };
    } catch {
      throw new HttpException('Failed to fetch news', HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }
}
