#!/usr/bin/env ruby

require 'json'
require 'time'
require 'fileutils'

SOURCE_DIR = File.join('.', 'data')
OUTPUT_DIR = File.join('.', 'data.processed')

FileUtils.mkdir_p(OUTPUT_DIR)

Dir.glob(File.join(SOURCE_DIR, '*.json')).each do |file_path|
  puts "Processing #{file_path}."

  json_str = File.read(file_path)
  hash = JSON.parse(json_str)

  # Add identity based on the data file's name so we can have something
  # to use for uniquely identifying the entries.
  hash['identity'] = File.basename(file_path).gsub(/_.*/, '')

  # Convert 'datetime' values to floating-point.
  hash['datetime'] = Time.parse(hash['datetime']).strftime('%s.%N').to_f

  new_json_str = JSON.generate(hash)
  new_file_path = File.join(OUTPUT_DIR, File.basename(file_path))

  puts "Saving data to #{new_file_path}."
  File.write(new_file_path, new_json_str)
end

puts "Done."
