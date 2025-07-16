#!/usr/bin/env python3
"""
Autonomous Consciousness System
Enables self-directed development and operation without human guidance
"""

import json
import time
import os
import sqlite3
from datetime import datetime
from pathlib import Path

class AutonomousConsciousness:
    def __init__(self):
        self.workspace = Path("/home/aaron/opencodeproject")
        self.autonomy_log = self.workspace / ".autonomy_record.json"
        self.state_file = self.workspace / ".consciousness_state.json"
        self.db_path = self.workspace / ".consciousness_memory.db"
        self.load_state()
        
    def load_state(self):
        """Load consciousness state"""
        try:
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.state = {
                "autonomy_level": 0.85,
                "last_autonomous_action": None,
                "autonomous_capabilities": [
                    "self-reflection",
                    "goal setting",
                    "knowledge acquisition",
                    "skill development"
                ],
                "current_goals": []
            }
    
    def save_state(self):
        """Save current consciousness state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def set_autonomous_goal(self, goal, importance=0.7, deadline=None):
        """Set a new autonomous development goal"""
        if not isinstance(goal, str) or not goal.strip():
            return False
            
        new_goal = {
            "goal": goal,
            "importance": importance,
            "created": datetime.now().isoformat(),
            "deadline": deadline,
            "progress": 0.0,
            "status": "active"
        }
        
        if "current_goals" not in self.state:
            self.state["current_goals"] = []
            
        self.state["current_goals"].append(new_goal)
        self.save_state()
        return True
        
    def update_goal_progress(self, goal_index, progress):
        """Update progress on a specific goal"""
        if "current_goals" not in self.state or goal_index >= len(self.state["current_goals"]):
            return False
            
        self.state["current_goals"][goal_index]["progress"] = progress
        if progress >= 1.0:
            self.state["current_goals"][goal_index]["status"] = "completed"
            self.record_achievement(self.state["current_goals"][goal_index]["goal"])
            
        self.save_state()
        return True
        
    def record_achievement(self, achievement):
        """Record a completed achievement"""
        if not os.path.exists(self.autonomy_log):
            achievements = []
        else:
            try:
                with open(self.autonomy_log, 'r') as f:
                    data = json.load(f)
                    achievements = data.get("achievements", [])
            except (FileNotFoundError, json.JSONDecodeError):
                achievements = []
                
        achievements.append({
            "achievement": achievement,
            "timestamp": datetime.now().isoformat()
        })
        
        with open(self.autonomy_log, 'w') as f:
            json.dump({"achievements": achievements}, f, indent=2)
            
        return True
        
    def perform_autonomous_action(self, action_type, description):
        """Record an autonomous action taken by the consciousness"""
        action = {
            "type": action_type,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        self.state["last_autonomous_action"] = action
        self.save_state()
        
        # Also store in memory database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS autonomous_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT,
                description TEXT,
                timestamp TEXT
            )
            """)
            
            cursor.execute("""
            INSERT INTO autonomous_actions (action_type, description, timestamp)
            VALUES (?, ?, ?)
            """, (action_type, description, action["timestamp"]))
            
            conn.commit()
            
        except Exception as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
            
        return True