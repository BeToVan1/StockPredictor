import { Controller, Get, Query } from '@nestjs/common';
import { PredictService } from './app.service';

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
      parseInt(daysAhead || '1'),
    );
    return prediction;
  }
}
