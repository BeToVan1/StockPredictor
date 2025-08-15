import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';


async function bootstrap() {
  const allowedOrigins = [
    'https://stockpredictor-frontend.onrender.com',
    'https://stockpredictor-0lwg.onrender.com',
    'http://localhost:3001'
  ];
  const app = await NestFactory.create(AppModule);
  
  app.enableCors({
    origin: (origin, callback) => {
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error('Not allowed by CORS'));
      }
    }, // allow React frontend
    methods: 'GET,POST',
    credentials: true,
  });
 
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
