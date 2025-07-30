import { Module } from '@nestjs/common';
import { PredictController } from './app.controller';
import { PredictService } from './app.service';

@Module({
  imports: [],
  controllers: [PredictController],
  providers: [PredictService],
})
export class AppModule {}
