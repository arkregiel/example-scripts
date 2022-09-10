# tcp_client.rb
# prosty klient TCP
# łączy się z serwerem,
# pobiera wiadomość od użytkowanika
# (z klawiatury),
# wysyła wiadomość do serwera,
# odbiera odpowiedx,
# wypisuje ją i zamyka połączenie

require "socket"

# nazwa hosta serwera
hostname = '127.0.0.1'

# numer portu serwera
port = 8080

# połączenie z serwerem
conn = TCPSocket.open hostname, port

# wypisanie znaku zachęty
print "> "

# pobranie wiadomości od użytkownik
msg = gets.chomp

# wysłanie wiadomości do serwera
conn.puts msg

puts "Sent"

# odebranie odpowiedzi od serwera
msg = conn.read

# wypisanie odpowiedzi serwera
puts "Server: #{msg}"

# zamknięcie połączenia
conn.close