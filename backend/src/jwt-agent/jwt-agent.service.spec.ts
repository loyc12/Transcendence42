import { Test, TestingModule } from '@nestjs/testing';
import { JwtAgent } from './jwt-agent.service';

describe('JwtAgentService', () => {
  let service: JwtAgent;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [JwtAgent],
    }).compile();

    service = module.get<JwtAgent>(JwtAgent);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
