import { WebSocketGateway, SubscribeMessage, OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect, WebSocketServer, MessageBody, ConnectedSocket } from '@nestjs/websockets';
import { Namespace, Server, Socket } from 'socket.io';

//@WebSocketGateway(3000, {
//  path: '/chat_ws'
//})
//@WebSocketGateway({
//  namspace: 'chat_ws'
//})
@WebSocketGateway()
export class ChatGateway implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect {

  //private server: Namespace;

  @WebSocketServer()
  server: Server;
  
  
  @SubscribeMessage('chat')
  handleMessage(@MessageBody() body: any, @ConnectedSocket() client: Socket): any {
    this.server.emit('chat', body);
//    return ({
//      event: 'pong',
//      data: 'I am a very special boy. din ding ding.'
//    });
  }

  afterInit(server: Server) {
//    this.server = server.of('/chat_ws')
    console.log('Gateway initialized');
    console.log('sockets: ', this.server.sockets);
    console.log('message event listeners : ', this.server.listeners('chat'));
  }

  handleConnection(client: any, ...args: any[]) {
    console.log('New Gateway Client Connected with args : ', args);
  }
  
  handleDisconnect(client: any) {
    console.log('A Gateway Client disconnected');
  }

  //@SubscribeMessage('message')
  //handleMessage(client: any, payload: any): string {
  //  this.server.emit('message', data);
  //  return 'Hello world!';
  //}
  
}
