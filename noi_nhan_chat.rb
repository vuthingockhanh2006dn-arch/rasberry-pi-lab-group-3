require 'mqtt'

MQTT::Client.connect('localhost') do |c|
  c.get('chat') do |topic, message|
    puts "[#{topic}] #{message}"
  end
end
