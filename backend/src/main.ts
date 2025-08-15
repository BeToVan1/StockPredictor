import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import * as express from 'express';
import { join } from 'path';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.enableCors({
    origin: 'http://localhost:3001', // allow React frontend
    methods: 'GET,POST',
    credentials: true,
  });
  app.use(express.static(join(__dirname, 'public')));
  app.getHttpAdapter().get('*', (req, res) => {
    res.sendFile(join(__dirname, '..', 'public', 'index.html'));
  });
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
