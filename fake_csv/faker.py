from faker import Faker

faker = Faker()


def get_fake_data(column_type, from_num=None, to_num=None):
    """Function to get random data of desired type"""
    if column_type == 'Full name':
        return faker.name()
    elif column_type == 'Job':
        return faker.job()
    elif column_type == 'Email':
        return faker.email()
    elif column_type == 'Domain name':
        return faker.domain_name()
    elif column_type == 'Phone number':
        return faker.phone_number()
    elif column_type == 'Company name':
        return faker.company()
    elif column_type == 'Text':
        if from_num and to_num:
            sentences_num = faker.pyint(min_value=min(from_num, to_num),
                                        max_value=max(from_num, to_num))
            return faker.paragraph(nb_sentences=sentences_num,
                                   variable_nb_sentences=False)
        elif from_num:
            sentences_num = faker.pyint(min_value=from_num, max_value=10)
            return faker.paragraph(nb_sentences=sentences_num,
                                   variable_nb_sentences=False)
        elif to_num:
            sentences_num = faker.pyint(min_value=0, max_value=to_num)
            return faker.paragraph(nb_sentences=sentences_num,
                                   variable_nb_sentences=False)
        sentences_num = faker.pyint(min_value=0, max_value=10)
        return faker.paragraph(nb_sentences=sentences_num,
                               variable_nb_sentences=False)
    elif column_type == 'Integer':
        if from_num and to_num:
            return faker.pyint(min_value=min(from_num, to_num),
                               max_value=max(from_num, to_num))
        elif from_num:
            return faker.pyint(min_value=from_num, max_value=9999999999)
        elif to_num:
            return faker.pyint(min_value=0, max_value=to_num)
        return faker.random_int()
    elif column_type == 'Address':
        return faker.address().replace('\n', ' ')
    elif column_type == 'Date':
        return faker.date()

