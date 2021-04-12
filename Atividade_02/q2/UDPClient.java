import java.io.*;
import java.math.BigInteger;
import java.util.*;
import java.net.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.ByteBuffer;
import java.nio.file.Files;

/*
    Sistema de transferência de arquivos via UDP
    Desenvolvedores: Brendow e Lucas

    Classe:     Cliente

    Execução:   javac UDPClient.java
                java UDPClient
                Digite o IP do servidor
                Nome do arquivo

    Funcionamento:  O programa conecta o cliente ao servidor;
                    Envia o nome do arquivo ao servidor;
                    Seleciona o arquivo no sistema de arquivos;
                    Calcula o Md5 do arquivo completo;
                    Envia o Md5 para o servidor;
                    Inicia a transferência dos bytes;
                    E finaliza a execução ao final da transferência.
*/


public class UDPClient {

    DatagramSocket dgramSocket;
    DatagramPacket dgramPackage;
    int serverPort = 6666;
    InetAddress serverAddr;

    //método construtor
    public UDPClient(){
        try {
            // Recebe o comandos
            Scanner reader = new Scanner(System.in);

            //Cria socket de UDP
            this.dgramSocket = new DatagramSocket(this.serverPort);;
            
            // armazena o IP do destino
            System.out.println("IP Destino: ");
            String dstIP = reader.nextLine();
            // se conecta com o servidor
            this.serverAddr = InetAddress.getByName(dstIP);

            //roda o fluxo principal
            run();

        } catch (Exception e) {
            // TODO: handle exception
        }
    }

    //converte um vetor de bytes para uma string de Hexadecimais
    public StringBuilder convertToHexa(byte[] bytes){

        StringBuilder sb = new StringBuilder();
        
        for (int i = 0; i < bytes.length; i++) {
            
            sb.append(Integer
                    .toString((bytes[i] & 0xff) + 0x100, 16)
                    .substring(1));
        }

        return sb;
    }

    //realiza a criação do código de verificação (md5), 
    //para garantir a integridade do arquivo
    public String checksum(String fileName) throws Exception{
        InputStream fis =  new FileInputStream(fileName);

        byte[] buffer = new byte[1024];
        MessageDigest complete = MessageDigest.getInstance("MD5");
        int numRead;

        do {
            numRead = fis.read(buffer);
            if (numRead > 0) {
                complete.update(buffer, 0, numRead);
            }
        } while (numRead != -1);

        fis.close();

        StringBuilder sb = convertToHexa(complete.digest());
        
        return sb.toString();
    }

    // envia o pacote de dados para o servidor
    public void sendPackage (byte[] payload, int payloadSize){
        this.dgramPackage = new DatagramPacket(payload, payloadSize, this.serverAddr, this.serverPort);

        // envia o pacote
        try {
            this.dgramSocket.send(this.dgramPackage);
        } catch (Exception e) {
            //TODO: handle exception
        }
    }

    // divide o arquivo em buffers de 1024 bytes para enviá-los ao servidor
    public void splitFile(File f) throws IOException {
        
        int partCounter = 1;
        int sizeOfFiles = 1024;
        
        byte[] buffer = new byte[sizeOfFiles];

        String fileName = f.getName();

        if (fileName != null) {
            try (
                FileInputStream fis = new FileInputStream(f); 
                BufferedInputStream bis = new BufferedInputStream(fis)
            ) {
                String md5 = "";
                try {
                    //calcula o md5 do arquivo
                    md5 = checksum(fileName);   
                } catch (Exception e) {
                    //TODO: handle exception
                }
                
                System.out.println("Md5: " + md5);
                try {
                    Thread.sleep(100);
                    
                } catch (Exception e) {
                    //TODO: handle exception
                }
                //envia o md5 do arquivo total para o servidor
                byte[] byteArrayMd5 = md5.getBytes();
                sendPackage(byteArrayMd5, byteArrayMd5.length);
                
                //calcula a quantidade de pacotes a serem enviados
                long qtdOfPckg = (f.length()/buffer.length) + 1;
 
                System.out.println("Quantidade de pacotes: " + qtdOfPckg);
                
                //insere o Long no byte[]
                String qtdBuffer = String.valueOf(qtdOfPckg);
                try {
                    Thread.sleep(100);
                    
                } catch (Exception e) {
                    //TODO: handle exception
                }
                //envia o número de pacotes que o servidor deve ler
                sendPackage(qtdBuffer.getBytes(), qtdBuffer.getBytes().length);
                
                
                int bytesAmount = 0;
                while ((bytesAmount = bis.read(buffer)) > 0) {
                    try {
                        Thread.sleep(100);
                        
                    } catch (Exception e) {
                        //TODO: handle exception
                    }
                    sendPackage(buffer, bytesAmount);
                    System.out.println("payload: " + buffer);
    
                }
                System.out.println("Arquivo enviado com sucesso.");
            }
        } else {
            System.out.println("Não foi possível encontrar um arquivo com esse nome, digite um nome existente.");
        }
    }

    //execução inicial
    public void run() {

        Scanner reader = new Scanner(System.in);

        try {

            String resp = "";

            System.out.println("Digite o nome do arquivo e a extensão: ");
            String fileName = reader.nextLine();

            File f = new File(fileName);

            // transforma o nome do arquivo em bytes
            byte[] fileNameBytes = fileName.getBytes();

            // envia o nome do arquivo
            sendPackage(fileNameBytes, fileNameBytes.length);

            //divide o arquivo
            splitFile(f);

            /* libera o socket */
            dgramSocket.close();
        } catch (SocketException e) {
            System.out.println("Socket: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO: " + e.getMessage());
        }

    }
    
    public static void main(String[] args) {
        UDPClient client = new UDPClient();
    }
}
