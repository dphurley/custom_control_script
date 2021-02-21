import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.DeviceComponent import DeviceComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.EncoderElement import *
from Launchpad.ConfigurableButtonElement import ConfigurableButtonElement
import time
from itertools import chain
from _Framework.Util import find_if
import collections
import json
import os

try:
	from user import *
except ImportError:
	pass

class custom_control_script(ControlSurface):
	def __init__(self, c_instance):
		super(custom_control_script, self).__init__(c_instance)

		with self.component_guard():
			global _map_modes
			_map_modes = Live.MidiMap.MapMode

			self.config_directory_path = "/Users/danny/ableton-device-mappings/"

			self.write_config_files_if_missing()
			
			selected_track_devices = self.song().view.selected_track.devices
			
			selected_track_devices_by_name = {}
			for device in selected_track_devices:
				selected_track_devices_by_name[device.name] = str(device)

			self.log_message(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
			self.log_message(":::::: DEVICES BY NAME ::::::::::::::::::::::::::::::::::::::::")
			self.log_message(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
			self.log_message(selected_track_devices_by_name)

			midi_mappings = self.load_midi_mappings_from_files()

			self.log_message(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
			self.log_message(":::::: MIDI MAPPINGS ::::::::::::::::::::::::::::::::::::::::::")
			self.log_message(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
			

			# mappable_parameters = []
			# for index, parameter in enumerate(selected_device_parameters, start=1):
			# 	mappable_parameter = {
			# 		"name": parameter.name
			# 	}
			# 	mappable_parameters.append(mappable_parameter)
			
			# self.log_message(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
			# self.log_message(":::::: MAPPABLE PARAMETERS ::::::::::::::::::::::::::::::::::::")
			# self.log_message(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
			# self.log_message(json.dumps(mappable_parameters, sort_keys=True, indent=4))

			# EncoderElement(MIDI_CC_TYPE, 0, 1, _map_modes.absolute).connect_to(selected_device_parameters[3])

	def load_midi_mappings_from_files(self):
		midi_maps = {}

		for filename in os.listdir(self.config_directory_path)
			device_name = os.path.splitext(filename)
			midi_maps[device_name] = json.loads(open(filename))

		return midi_maps


	def write_config_files_if_missing(self):
		tracks_to_scan = [self.song().tracks, self.song().return_tracks]

		for track_list in tracks_to_scan:
			for track in track_list:
				self.log_message(":::::::::::::::::: Track Name: " + track.name + " ::::::::::::::")
				for device in track.devices:
					self.log_message("::::: device: " + device.class_name + " - " + device.name)
					
					if(not os.path.exists(self.config_directory_path)):
						self.log_message("::: CREATING DIRECTORY")
						os.mkdir(self.config_directory_path)
						
					device_filename = self.config_directory_path + device.name + ".json"
					
					if(os.path.exists(device_filename)):
						next
					else:
						self.log_message("::: WRITING CONFIG FILE FOR " + device.name)

						mappable_parameters = []
						for index, parameter in enumerate(device.parameters, start=1):
							mappable_parameter = {
								"name": parameter.name
							}
							mappable_parameters.append(mappable_parameter)

						device_config_file = open(device_filename, "w")
						device_config_file.write(json.dumps(mappable_parameters, sort_keys=True, indent=4))
						device_config_file.close()
