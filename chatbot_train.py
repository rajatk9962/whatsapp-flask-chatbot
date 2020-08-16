from chatterbot import ChatBot


from chatterbot.trainers import ListTrainer



def get_response(message):
    bot = ChatBot('bot')
    trainer = ListTrainer(bot)
    # Training 
    trainer.train(['CDC: Upgrade to EMC version 4.6 SP1 Patch 21 - Text that is entered over 255 bytes is not saved on the form in xEditor. xEditor text issue', '	Vendor provided hotfix.'])
    trainer.train(['Batch Job Performance Degraded after Patch 29 and Hotfix','null' ])
    trainer.train(['xEditor Tab Issue When form opens in xEditor, pressed tab key on keyboard to go to next field. Instead of going to next field, the text in the field is deleted, and then field is expanded.Expected to go to next editable field when pressing tab key ','Use Up Arrow and Down Arrow instead of tab'])
    trainer.train(['xEditor Name Not Bold CDC: Upgrade to EMC version 4.6 SP1 Patch 21 - Phone Number under the Adjuster Name is not bold in xEditor	xEditor Name Not Bold','Vendor provided hotfix.'])
    trainer.train(['Hidden Field Issue Upgrade to EMC version 4.6 SP1 Patch 21 - Issues when using xEditor - MD1 form having hidden editable field.There is a hidden editable field under Mercury Retained table which user can enter text in.','Still an issue Not working when optional paragraph is added'])
    trainer.train(['xEditor Document Action Document Actions is not displaying after install','Issue is resloved when Word settings are set based on vendor suggestions.'])
    trainer.train(['Restrict Editing issue Unable to edit form after removing Restrict Editing option Unable to enter in text when ‘Restrict Editing’ option is not selected.','Still an issue. Not able to remove Restrict Editing option from Review tab and enter text.'])
    trainer.train(['Slowness xEditor Window open slowness','Still an issue.It takes on average 20 seconds to open xEditor, It is up an average of 11 seconds from 4.5 version.'])
    trainer.train(['Optional Content issue Old WIP document created in xEditor 4.5 is not working in xEditor 4.6 for the select/un-select optional content. Optional Content issue','Still an issue'])

    reply=bot.get_response(message)
    return reply




