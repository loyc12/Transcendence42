import { Controller, Get, Res } from '@nestjs/common';
import { AppService } from './app.service';
import { Response } from 'express';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
  
  @Get('/germain')
  kingGermain(@Res() res: Response) {
    res.sendFile('/workspaces/Transcendence42/frontend/frame/index.html');//, { root: 'public' });
  }
}