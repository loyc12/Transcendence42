import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class JwtAgent {
    constructor(
        private config: ConfigService,
        private jwt: JwtService
    ) {}

    async signToken(userID: number, email: string, is_logged_in: boolean): Promise<{access_token: string}> {
        const payload = {
            sub: userID,
            email,
            is_logged_in
        };

        const token = await this.jwt.signAsync(payload);
        return ({
            access_token: token
        });
    }
}
