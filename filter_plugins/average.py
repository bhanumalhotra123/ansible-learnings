def average (list):
    return sum(list) / float(len(list))

class FilterModule(object):

    def filters(self):
        return {
            'average': average
        }
    



    # export ANSIBLE_FILTER_PLUGINS=/fi;ter_plugins;
      ansible-playbook playbook1.yml
    