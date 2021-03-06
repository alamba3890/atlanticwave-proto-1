# Copyright 2016 - Sean Donovan
# AtlanticWave/SDX Project


class UserPolicyTypeError(TypeError):
    pass

class UserPolicyValueError(ValueError):
    pass

class UserPolicy(object):
    ''' This is the interface between the SDX controller and the user-level 
        application. This will likely be heavily modified over the course of 
        development, more so than most other interfaces. '''

    def __init__(self, username, ruletype, json_rule):
        ''' Parses the json_rule passed in to populate the UserPolicy. '''
        self.username = username
        self.ruletype = ruletype
        self.json_rule = json_rule

        # The breakdown list should be a list of UserPolicyBreakdown objects.
        self.breakdown = None
        self.rule_hash = None

        # All rules should have start and stop times. They may be rediculously
        # far in the past and/or the future, but the should have them.
        # They should be strings in rfc3339format (see shared.constants).
        self.start_time = None
        self.stop_time = None

        # Now that all the fields are set up, parse the json.
        self._parse_json(self.json_rule)


    @staticmethod
    def check_syntax(json_rule):
        ''' Used to validate syntax of json user rules before they are parsed.
            Must be implemented by child classes. '''
        raise NotImplementedError("Subclasses must implement this.")

    def breakdown_rule(self, topology, authorization_func):
        ''' Called by the BreakdownEngine to break a user rule apart. Should
            only be called by the BreakdownEngine, which passes the topology
            and authorization_func to it.
            Returns a list of UserPolicyBreakdown objects.
            Must be implemented by child classes. '''
        raise NotImplementedError("Subclasses must implement this.")

    def check_validity(self, topology, authorization_func):
        ''' Called by the ValidityInspector to check if the particular object is
            valid. Should only be called by the ValidityInspector, which passes
            the topology and authorization_func to it. ''' 
        raise NotImplementedError("Subclasses must implement this.")

    def set_breakdown(self, breakdown):
        self.breakdown = breakdown

    def get_breakdown(self):
        return self.breakdown

    def get_start_time(self):
        return self.start_time

    def get_stop_time(self):
        return self.stop_time

    def get_json_rule(self):
        return self.json_rule

    def get_ruletype(self):
        return self.ruletype

    def get_user(self):
        return self.username

    def set_rule_hash(self, hash):
        self.rule_hash = hash

    def get_rule_hash(self):
        return self.rule_hash



    def _parse_json(self, json_rule):
        ''' Actually does parsing. 
            Must be implemented by child classes. '''
        raise NotImplementedError("Subclasses must implement this.")


        
class UserPolicyBreakdown(object):
    ''' This provides a standard way of holding broken down rules. Captures the
        local controller and the rules passed to them. '''

    def __init__(self, lc, list_of_rules=[]):
        ''' The lc is the shortname of the local controller. The list_of_rules 
            is a list of rules that are being sent to the Local Controllers. '''
        self.lc = lc
        self.rules = list_of_rules

    def get_lc(self):
        return self.lc

    def get_list_of_rules(self):
        return self.rules

    def add_to_list_of_rules(self, rule):
        self.rules.append(rule)
