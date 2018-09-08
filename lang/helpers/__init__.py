# coding: utf-8


def create_lang_dir(self, name='default', title='Default'):

    fs_app = self.fs_app
    fs_package = self.fs_pkg

    path = '/resources/lang/{}/'.format(name)

    if not fs_app.exists(path):
        fs_lang = fs_app.makedirs(path)
    else:
        fs_lang = fs_app.opendir(path)

    status = False
    if fs_lang.isempty('.'):

        filename = '__init__.py'
        template = fs_package.gettext('/snippets/resources/lang/default/' + filename)
        template = template.format(name=name, title=title)

        fs_lang.create(filename)
        lang = fs_lang.open(filename, mode='w')
        lang.write(template)
        lang.close()

        self.quiet or self.info('Installed {}'.format(path))
        status = True
    else:
        self.quiet or self.info('{} already exists'.format(path))

    fs_lang.close()

    return status
