require 'mqtt'
require 'thread'

print "Nhap ten cua ban: "
name = gets.chomp

client = MQTT::Client.connect('localhost')

Thread.new do
  client.get('chat') do |_topic, message|
    puts "\n#{message}"
    print "> "
  end
end

loop do
  print "> "
  msg = gets.chomp
  break if msg.downcase == 'exit'

  client.publish('chat', "#{name}: #{msg}")
end

client.disconnect
