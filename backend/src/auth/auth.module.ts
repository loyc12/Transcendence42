import { Module } from "@nestjs/common";
import { AuthController } from "./auth.controller";
import { AuthService } from "./auth.service";
import { PrismaModule } from "src/prisma/prisma.module";
import { JwtModule } from "@nestjs/jwt";
import { JwtStrategy } from "src/auth/strategy/jwt.strategy";
import { JwtAgent } from "src/jwt-agent/jwt-agent.service";

@Module({
    imports: [JwtModule.register({
        global: true,
        secret: process.env['JWT_SECRET'],
        signOptions: { expiresIn: '1d' },
      }),],
    controllers: [AuthController],
    providers: [AuthService, JwtStrategy, JwtAgent]
})
export class AuthModule {}