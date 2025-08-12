import { Module } from '@nestjs/common';
import {ConfigModule} from '@nestjs/config';
import { PredictController, NewsController } from './app.controller';
import { PredictService, NewsService } from './app.service';

@Module({
  imports: [ConfigModule.forRoot()],
  controllers: [PredictController, NewsController],
  providers: [PredictService, NewsService],
})
export class AppModule {}
