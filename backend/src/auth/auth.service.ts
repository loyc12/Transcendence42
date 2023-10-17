import { ForbiddenException, Injectable, InternalServerErrorException } from '@nestjs/common';
//import { ConfigService } from '@nestjs/config';
import { User } from '@prisma/client';
import { PrismaService } from 'src/prisma/prisma.service';
import * as argon from "argon2"
import { AuthDto } from './dto';
import { PrismaClientKnownRequestError } from '@prisma/client/runtime/library';
import { JwtAgent } from 'src/jwt-agent/jwt-agent.service';

@Injectable()
export class AuthService {
    constructor(
        private prisma: PrismaService,
        private jwt: JwtAgent,
//        private config: ConfigService
    ) {}

    index(request: Request) {
        console.log("Request headers : ", request.headers);
        return ("Transcendence Authentication endpoint reached.");
    }

    async signup(dto: AuthDto): Promise<User> {
        const hash: Promise<string> = argon.hash(dto.password);
        const userCreateData: any = {
            data: {
                username: dto.userName,
                email: dto.email,
                hash: await hash,
                firstName: dto.firstName,
                lastName: dto.lastName,
            }
        }
        console.log('My Hash : ', hash);
        console.log('My userCreateData : ', userCreateData);
        try {
            const user = await this.prisma.user.create(userCreateData);
            delete user.hash;
            return (user);
        } catch (error) {
            if (error instanceof PrismaClientKnownRequestError
                && error.code == 'P2002')
                throw new ForbiddenException('Credentials already taken');
            else
                throw new InternalServerErrorException('Unknown server error occured while fetching database info. error code : ');
        }

        // TODO =>> Initiate 42oauth process and login user.
    }

    async deleteUser(dto: AuthDto) {
        const user: User = await this.prisma.user.findUnique({
            where: {
                username: dto.userName,
            }
        })
        if (!user) {
            throw new ForbiddenException('Credentials incorrect')
        }
        else if (!(await argon.verify(user.hash, dto.password))) {
            throw new ForbiddenException('Credentials incorrect')
        }
        delete user.hash;
        await this.prisma.user.delete({
            where: {
                username: dto.userName,
                //hash: await hash
            }
        })
        return (`User ${dto.userName} successfully deleted.`);
    }

    async signin(dto: AuthDto) {

        const user: User = await this.prisma.user.findUnique({
            where: {
                username: dto.userName,
            }
        })
        if (!user) {
            throw new ForbiddenException('Credentials incorrect')
        }
        else if (!(await argon.verify(user.hash, dto.password))) {
            throw new ForbiddenException('Credentials incorrect')
        }
        delete user.hash;

        const token = this.jwt.signToken(user.id, user.email, true);
        console.log('User authenticated : ', user);
        console.log('User jwt token : ', token);
        return (token);
        //return (user);
    }
}
