

/**
 * UDPClient: Cliente UDP Descricao: Envia uma msg em um datagrama e recebe a
 * mesma msg do servidor
 */


public class UDPClient {
    public static void main(String args[]) {
        ThreadSender ts = new ThreadSender();
        ThreadReceiver tr = new ThreadReceiver();

        ts.start();
        tr.start();
    } //main	
}
