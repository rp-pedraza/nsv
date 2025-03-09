#!/usr/bin/env ruby

# Usage: [ruby] ./process-data.rb [source_dir [output_dir]]
#
# Default source_dir is './data'.  Default output_dir is '(source_dir).processed'.

require 'json'
require 'time'
require 'fileutils'

default_data_dir = File.join(__dir__, '..', 'data')
source_dir = ARGV.shift || DEFAULT_DATA_DI
output_dir = ARGV.shift || source_dir + '.processed'

raise "Data directory '#{source_dir}' doesn't exist.") unless File.directory?(source_dir)
FileUtils.mkdir_p(output_dir)
files = Dir.glob(File.join(source_dir, '*.json'))
raise "No data file found in '#{source_dir}'" if files.empty?

files.each do |file_path|
  puts "Processing #{file_path}."

  json_str = File.read(file_path)
  hash = JSON.parse(json_str)

  # Add identity based on the data file's name so we can have something
  # to use for uniquely identifying the entries.
  hash['identity'] = File.basename(file_path).gsub(/_.*/, '')

  # Convert 'datetime' values to floating-point.
  hash['datetime'] = Time.parse(hash['datetime']).strftime('%s.%N').to_f

  new_json_str = JSON.generate(hash)
  new_file_path = File.join(output_dir, File.basename(file_path))

  puts "Saving data to #{new_file_path}."
  File.write(new_file_path, new_json_str)
end

puts "Done."
