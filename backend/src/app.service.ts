import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    //return 'WOWOW World!';
    return `<h1>Wow World Incroyable !</h1>`
  }
}
