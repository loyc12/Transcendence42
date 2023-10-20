import { Injectable, InternalServerErrorException } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { PrismaClient, User } from "@prisma/client";

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
    //async _getUserEntry(queryObj)

    async getUserEntry(userID: number, with_hash_pw: boolean = false): Promise<User> | null {
        let user: User = await this.user.findUnique({
            where: {
                id: userID
            }
        })
        if (!user)
            return (null);
        if (!with_hash_pw)
            delete user.hash;
        return (user);
    }

    async getUserEntryStrict(userID: number, with_hash_pw: boolean = false): Promise<User> | null {
        const user: User = await this.getUserEntry(userID);
        if (!user)
            throw new InternalServerErrorException('No user exist with given userID.');
        return (user);
    }

    // Check that the user went through the authentication process and is logged in. With corresponding setter.
    async checkIsUserAuthenticated(userID: number): Promise<boolean> {
        const user: User = await this.getUserEntryStrict(userID);
        return (user.isAuthenticated);
    }
    async setUserAuthenticatedStatus(userID: number, status: boolean) {
        let user: User = await this.getUserEntryStrict(userID);
        user.isAuthenticated = status;
    }
}