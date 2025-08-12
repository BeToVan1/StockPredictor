import { Test, TestingModule } from '@nestjs/testing';
import { PredictController, NewsController } from './app.controller';
import { PredictService, NewsService } from './app.service';

describe('PredictController', () => {
  let controller: PredictController;
  let service: PredictService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [PredictController],
      providers: [
        {
          provide: PredictService,
          useValue: {
            predict: jest.fn().mockResolvedValue({ prediction: 123 }),
          },
        },
      ],
    }).compile();

    controller = module.get<PredictController>(PredictController);
    service = module.get<PredictService>(PredictService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  it('should return a prediction', async () => {
    const result = await controller.getPrediction('AAPL', '60', '5');
    expect(result).toEqual({ prediction: 123 });
    expect(service.predict).toHaveBeenCalledWith('AAPL', 60, 5);
  });
});

describe('NewsController', () => {
  let controller: NewsController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [NewsController],
    }).compile();

    controller = module.get<NewsController>(NewsController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

});
