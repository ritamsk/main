import sys
import os
import xmlschema
import lxml.etree as ET
import logging

logging.basicConfig(filename="logs.log", level=logging.INFO)


if __name__ == "__main__":
    logging.info("Program started")
    params = sys.argv
    if len(params)<4:
        logging.error('not enought arguments')
    elif len(params)>5:
        logging.error('too many arguments')
    else:
        count = 0
        if os.path.exists(params[1]):
            xml_file = ET.parse(params[1])
            count+=1
        else:
            logging.error('wrong xml file path')

        if os.path.exists(params[2]):
            schema = xmlschema.XMLSchema(params[2])
            count += 1
        else:
            logging.error('wrong xsd file path')

        if os.path.exists(params[3]):
            xslt = ET.parse(params[3])
            count += 1
        else:
            logging.error('wrong xslt file path')


        if count==3: # if all files are given

            if schema.is_valid(xml_file):
                transform = ET.XSLT(xslt)
                new_xml = transform(xml_file)
                logging.info("transformation complited successfully")
                if schema.is_valid(new_xml):
                    logging.info('nem transformed xml file is valid')
                    result_flename = params[1].split(os.path.basename(params[1]))[0]
                    if len(params) == 5:
                        result_flename += str(params[4]).replace('.', '').replace('/', '') + '.xml'
                    else:
                        result_flename += os.path.basename(params[1]).split('.')[0] + '_lstm.xml'

                    with open(result_flename, 'w') as f:
                        f.write(str(new_xml))
                        logging.info('all done successfully')
                else:
                    logging.error('transformed xml is not valid')
            else:
                logging.error('input xml is not valid')
        else:
            logging.error('not all files are given')

    logging.info("Program ended")