#!/usr/bin/python
import random
import sys
import os

def plyr_compare ( players , opponents , self_or_roster , bank ):
    player_stat_map = {}
    existing_choice = ""
    count           = 0
    price           = 0.0
    while count < len(players):
        stat_splt = players[count].split("|")
        if stat_splt[3] != "N":
            stat_splt_score = float(stat_splt[6]) + float(stat_splt[7]) - float(stat_splt[2]) - float(stat_splt[4]) - float(opponents[stat_splt[5]])
            player_stat_map[players[count]] = stat_splt_score
        else:
            player_stat_map[players[count]] = 0
        if existing_choice == "":
            score  = player_stat_map[players[count]]
            name   = stat_splt[0]
            price  = stat_splt[2]
            existing_choice = [name,score,price]
        else:
            if self_or_roster == "self":
                if existing_choice[1] > player_stat_map[players[count]]:
                    score  = player_stat_map[players[count]]
                    name   = stat_splt[0]
                    price  = float(bank) + float(stat_splt[2])
                    existing_choice = [name,score,price]
            else:
                if existing_choice[1] < player_stat_map[players[count]]:
                    price  = stat_splt[2]
                    if float(bank) > float(price):
                        score  = player_stat_map[players[count]]
                        name   = stat_splt[0]
                        existing_choice = [name,score,price]
                   
        count = count + 1
    return existing_choice
        
def opponent_toughness ( teams ):
    tufnes_map  = {}
    opponents   = teams.split(":")
    oppnt_list  = opponents[1].split(",")
    counter     = 0
    oppnt_count = len(oppnt_list)
    for oppnt in oppnt_list:
        oppnt = oppnt.strip()
        tufnes_map [oppnt] = oppnt_count - counter
        counter = counter + 1
    return tufnes_map

def parser ( position , roster ):
    self_flag      = 0
    is_roster      = 0
    roster_flag    = 0
    inp_file       = open('stats.txt')
    line           = inp_file.readline()
    oppnt_tufnes   = {}
    my_team_flag   = 0
    my_team        = []
    roster_options = []
    my_team_stats  = []
    bank           = 0 
   
    while line:
        if ("Bank" in line):
            line = line.split(":")
            bank = line[1].strip()     
        if ("teams" in line):
            oppnt_tufnes = opponent_toughness(line)
        if ("|" in line):
            plyr    = line.split("|")
            plyr[0] = plyr[0].strip()
            if len(my_team) > 0:
                for self in my_team:
                    if plyr[0] in self:
                        my_team_stats.append(line)
                        is_roster = 0
                        break
                    else:
                        is_roster = 1  
                if ("player" != plyr[0]) and (plyr[1] == position) and is_roster == 1:
                    roster_options.append(line)
        if my_team_flag == 1 and roster in line:
            splt         = line.split(":")
            my_team      = splt[1].split(",")
            my_team_flag = 0
            roster_flag  = 1
        if ("My_team" in line):
            my_team_flag = 1
        elif roster_flag == 1:
            my_team_flag = 0
        line = inp_file.readline()
        
    inp_file.close()
    recursor_flag = {}
    replace       = plyr_compare (my_team_stats , oppnt_tufnes, "self" , bank)
    bnk_aftr_rplc = replace[2]
    best_roster   = plyr_compare (roster_options , oppnt_tufnes , "roster" , bnk_aftr_rplc)
    print "replace %s " %replace
    print "with %s \n" %best_roster
    
def fpl_advisor ():
    positions = {"G":"Goal Keeper","D":"Defender","M":"Midfielder","F":"Forward"}
    for keys in positions:
        print "In position -- %s" %positions[keys]
        parser( keys , positions[keys])

fpl_advisor ()
