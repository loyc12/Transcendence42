import { Body, Controller, Get, Req } from '@nestjs/common';
import { AuthService } from './auth.service';
import { AuthDto } from './dto';

@Controller('auth')
export class AuthController {
    constructor (private authService: AuthService) {}

    @Get()
    index(@Req() request: Request) {
        return (this.authService.index(request));
    }

    @Get('/sign_doe')
    signupJohnDoe() {
        const dto: AuthDto = {
            userName: 'John Doe',
            password: 'KarmeleonJoviale',
            email: 'onfaitletwist@america.us',
            firstName: 'John',
            lastName: 'Doe'
        }
        return (this.authService.signup(dto));
    }

    @Get('/delete_doe')
    deleteJohnDoe() {
        const dto: AuthDto = {
            userName: 'John Doe',
            password: 'KarmeleonJoviale',
            email: 'onfaitletwist@america.us',
            firstName: 'John',
            lastName: 'Doe'
        }
        return (this.authService.deleteUser(dto));
    }
}
