import { IsEmail, IsNotEmpty, IsOptional, IsString, IsStrongPassword } from "class-validator";

export class AuthDto {

    @IsString()
    @IsNotEmpty()
    userName: string;
    
    @IsString()
    @IsNotEmpty()
    @IsStrongPassword()
    password: string;

    @IsString()
    @IsNotEmpty()
    @IsEmail()
    @IsOptional()
    email: string;

    @IsString()
    @IsOptional()
    firstName: string;

    @IsString()
    @IsOptional()
    lastName: string;    
}