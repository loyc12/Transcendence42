import { Test, TestingModule } from '@nestjs/testing';
import { JwtAgentService } from './jwt-agent.service';

describe('JwtAgentService', () => {
  let service: JwtAgentService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [JwtAgentService],
    }).compile();

    service = module.get<JwtAgentService>(JwtAgentService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
