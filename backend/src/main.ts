import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { ChatGateway } from './chat-gateway/chat-gateway.gateway';

const listen_port: string = '3000';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true
  }))
  await app.listen(listen_port);
}
bootstrap();
