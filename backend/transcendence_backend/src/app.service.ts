import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    let ret: string = '';
    ret += "<p>Regarde ma belle string comme c\'est beau ça.</p>"
    ret += "<p>Pi quin, en vla une autre. </p>"
    ret += "<p>Coudonc, ça arrête pu st'affaire là. </p>"
    return ret;
  }
}
