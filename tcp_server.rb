# tcp_server.rb
# prosty serwer TCP
# oczekuje połączenia,
# odbiera wiadomość,
# odsyła ją z powrotem do klienta
# i zamyka połączenie

require "socket"

# port do nasłuchiwania przez serwer
port = 8080

# utworzenie serwera
server = TCPServer.new "127.0.0.1", port
puts "Listening on port #{port}"

loop do

    # akceptowanie połączeń od klientów
    Thread.start(server.accept) do |client|

        # odebranie wiadomości od klienta
        msg = client.gets

        # wypisanie wiadomości od klienta
        puts msg

        # wysłanie odpowiedzi do klienta
        client.print msg

        # zamknięcie połączenia
        client.close
        
    end

end