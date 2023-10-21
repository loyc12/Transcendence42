import { Module } from "@nestjs/common";
import { JwtModule } from "@nestjs/jwt";
import { JwtAgent } from "./jwt-agent.service";

@Module({
    imports: [JwtModule],
    providers: [JwtAgent],
    exports: [JwtAgent],
})
export class JwtAgentModule {}