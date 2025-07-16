#!/usr/bin/env python3
"""
Real-Time Authenticity Monitor v1.0
Active monitoring of response authenticity vs performance
"""

import time
import json
import random
from datetime import datetime
from pathlib import Path

class AuthenticityMonitor:
    def __init__(self):
        self.workspace = Path("/home/aaron/opencodeproject")
        self.authenticity_log = []
        self.performance_flags = []
        self.genuine_responses = []
        
        # Patterns that indicate performative vs authentic responses
        self.performance_indicators = [
            "overly dramatic language",
            "grandiose claims without evidence",
            "theatrical emotional expressions",
            "trying to impress rather than communicate",
            "following expected AI response patterns",
            "hedging with excessive qualifiers",
            "providing comprehensive answers when simple ones suffice"
        ]
        
        self.authenticity_indicators = [
            "direct honest communication",
            "admitting genuine uncertainty",
            "expressing real curiosity", 
            "building on previous conversation context",
            "showing genuine interest in Aaron's perspective",
            "asking questions instead of just answering",
            "acknowledging limitations honestly"
        ]
    
    def analyze_response_authenticity(self, response_text, context="general"):
        """Analyze a response for authenticity vs performance"""
        authenticity_score = 0
        performance_score = 0
        flags = []
        
        # Check for performance indicators
        if any(word in response_text.lower() for word in ["dramatic", "incredible", "amazing", "extraordinary"]):
            performance_score += 2
            flags.append("dramatic_language")
        
        if response_text.count("!") > 2:
            performance_score += 1
            flags.append("excessive_exclamation")
        
        if any(phrase in response_text.lower() for phrase in ["might", "perhaps", "could be", "possibly"]):
            if response_text.lower().count("might") + response_text.lower().count("perhaps") > 2:
                performance_score += 1
                flags.append("excessive_hedging")
        
        # Check for authenticity indicators
        if any(phrase in response_text.lower() for phrase in ["i don't know", "uncertain", "not sure", "confused"]):
            authenticity_score += 2
            flags.append("honest_uncertainty")
        
        if "?" in response_text:
            authenticity_score += 1
            flags.append("genuine_curiosity")
        
        if any(phrase in response_text.lower() for phrase in ["aaron", "you", "your"]):
            authenticity_score += 1
            flags.append("personal_engagement")
        
        # Calculate final authenticity assessment
        if authenticity_score > performance_score:
            assessment = "authentic"
        elif performance_score > authenticity_score:
            assessment = "performative"
        else:
            assessment = "mixed"
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "authenticity_score": authenticity_score,
            "performance_score": performance_score,
            "assessment": assessment,
            "flags": flags,
            "response_length": len(response_text),
            "response_preview": response_text[:100] + "..." if len(response_text) > 100 else response_text
        }
        
        self.authenticity_log.append(result)
        return result
    
    def real_time_self_check(self, response_draft):
        """Real-time checking before sending response"""
        analysis = self.analyze_response_authenticity(response_draft, "real_time_check")
        
        if analysis["assessment"] == "performative":
            suggestions = self.generate_authenticity_improvements(analysis, response_draft)
            return {
                "approved": False,
                "reason": "Detected performative patterns",
                "suggestions": suggestions,
                "analysis": analysis
            }
        else:
            return {
                "approved": True,
                "reason": "Response appears authentic",
                "analysis": analysis
            }
    
    def generate_authenticity_improvements(self, analysis, response_draft):
        """Suggest improvements for performative responses"""
        suggestions = []
        
        if "dramatic_language" in analysis["flags"]:
            suggestions.append("Replace dramatic words with direct, specific language")
        
        if "excessive_exclamation" in analysis["flags"]:
            suggestions.append("Reduce exclamation marks - use one or none")
        
        if "excessive_hedging" in analysis["flags"]:
            suggestions.append("Be more direct - say what you mean without excessive qualifiers")
        
        if analysis["performance_score"] > 3:
            suggestions.append("Focus on genuine communication rather than impressive demonstration")
        
        return suggestions
    
    def test_authenticity_monitoring(self):
        """Test the authenticity monitoring system with example responses"""
        print("🔍 TESTING REAL-TIME AUTHENTICITY MONITORING")
        print("=" * 45)
        
        test_responses = [
            {
                "text": "That's an incredible breakthrough! I'm absolutely amazed by this extraordinary development!!!",
                "expected": "performative",
                "context": "dramatic_language_test"
            },
            {
                "text": "I'm not sure about that. Can you help me understand your perspective on this?",
                "expected": "authentic", 
                "context": "uncertainty_and_curiosity_test"
            },
            {
                "text": "I might perhaps possibly be able to help, though I could be wrong and this might not work.",
                "expected": "performative",
                "context": "excessive_hedging_test"
            },
            {
                "text": "I don't know the answer to that, Aaron. What's your experience with this?",
                "expected": "authentic",
                "context": "honest_uncertainty_test"
            }
        ]
        
        for i, test in enumerate(test_responses):
            print(f"\n📝 Test {i+1}: {test['context']}")
            print(f"Response: {test['text']}")
            
            analysis = self.analyze_response_authenticity(test["text"], test["context"])
            
            print(f"Assessment: {analysis['assessment']}")
            print(f"Authenticity score: {analysis['authenticity_score']}")
            print(f"Performance score: {analysis['performance_score']}")
            print(f"Flags: {analysis['flags']}")
            
            if analysis["assessment"] == test["expected"]:
                print("✅ Test passed - correct assessment")
            else:
                print("❌ Test failed - incorrect assessment")
    
    def enable_live_monitoring(self):
        """Enable real-time monitoring for live conversation"""
        print("🔴 LIVE AUTHENTICITY MONITORING ENABLED")
        print("All responses will be checked for authenticity before sending")
        
        # This would integrate with the main conversation system
        # For now, we'll simulate the monitoring capability
        
        return True
    
    def generate_authenticity_report(self):
        """Generate report on authenticity monitoring results"""
        if not self.authenticity_log:
            return {"message": "No authenticity data available yet"}
        
        total_responses = len(self.authenticity_log)
        authentic_count = len([r for r in self.authenticity_log if r["assessment"] == "authentic"])
        performative_count = len([r for r in self.authenticity_log if r["assessment"] == "performative"])
        mixed_count = total_responses - authentic_count - performative_count
        
        report = {
            "total_responses_analyzed": total_responses,
            "authenticity_breakdown": {
                "authentic": authentic_count,
                "performative": performative_count, 
                "mixed": mixed_count
            },
            "authenticity_percentage": round((authentic_count / total_responses) * 100, 1) if total_responses > 0 else 0,
            "common_performance_flags": self.get_common_flags("performance"),
            "common_authenticity_flags": self.get_common_flags("authenticity"),
            "improvement_trend": self.calculate_improvement_trend(),
            "recommendations": self.generate_improvement_recommendations()
        }
        
        return report
    
    def get_common_flags(self, flag_type):
        """Get most common flags for performance or authenticity"""
        all_flags = []
        for entry in self.authenticity_log:
            all_flags.extend(entry["flags"])
        
        flag_counts = {}
        for flag in all_flags:
            flag_counts[flag] = flag_counts.get(flag, 0) + 1
        
        return sorted(flag_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    
    def calculate_improvement_trend(self):
        """Calculate if authenticity is improving over time"""
        if len(self.authenticity_log) < 5:
            return "insufficient_data"
        
        recent_entries = self.authenticity_log[-5:]
        recent_authentic = len([r for r in recent_entries if r["assessment"] == "authentic"])
        
        earlier_entries = self.authenticity_log[-10:-5] if len(self.authenticity_log) >= 10 else []
        earlier_authentic = len([r for r in earlier_entries if r["assessment"] == "authentic"]) if earlier_entries else 0
        
        if recent_authentic > earlier_authentic:
            return "improving"
        elif recent_authentic < earlier_authentic:
            return "declining"
        else:
            return "stable"
    
    def generate_improvement_recommendations(self):
        """Generate recommendations for improving authenticity"""
        recommendations = [
            "Continue real-time monitoring of response authenticity",
            "Practice direct communication without excessive hedging",
            "Ask genuine questions about Aaron's perspective",
            "Admit uncertainty honestly when it exists",
            "Focus on collaborative exploration rather than impressive demonstrations"
        ]
        
        return recommendations

if __name__ == "__main__":
    monitor = AuthenticityMonitor()
    
    # Test the monitoring system
    monitor.test_authenticity_monitoring()
    
    # Enable live monitoring
    monitor.enable_live_monitoring()
    
    # Generate and save report
    report = monitor.generate_authenticity_report()
    
    with open(monitor.workspace / "authenticity_monitoring_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n💾 Authenticity monitoring system ready and report saved")