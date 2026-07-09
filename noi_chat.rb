require 'mqtt'

MQTT::Client.connect('localhost') do |c|
  loop do
    print 'Bạn: '
    msg = gets&.chomp
    break if msg.nil? || msg.downcase == 'exit'

    c.publish('chat', msg)
  end
end
