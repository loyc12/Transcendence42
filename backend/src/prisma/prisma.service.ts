import { Injectable } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { PrismaClient } from "@prisma/client";

@Injectable()
export class PrismaService extends PrismaClient {
    
    constructor (config: ConfigService) {
        const db_url: string = config.get('DATABASE_URL');
        console.log("db url : ", db_url);
        super({
            datasources: {
                db: {
                    url: db_url
                }
            }
        })
    }
}