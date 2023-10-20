import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PrismaModule } from './prisma/prisma.module';
import { AuthModule } from './auth/auth.module';
import { JwtAgentModule } from './jwt-agent/jwt-agent.module';
import { ConfigModule } from '@nestjs/config';
//import { JwtAgent } from './jwt-agent/jwt-agent.service';
import { ChatGateway } from './chat-gateway/chat-gateway.gateway';

@Module({
  imports: [
    PrismaModule,
    AuthModule,
    JwtAgentModule,
    ConfigModule.forRoot({
      isGlobal: true
    })
  ],
  controllers: [AppController],
  providers: [AppService, ChatGateway],
})
export class AppModule {}
