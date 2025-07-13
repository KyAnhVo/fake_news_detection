import csv  


with (
        open(file= "./model/training_dataset/True.csv") as og,
        open(file= "./model/training_dataset/True_train.csv", mode= "w") as train_file,
        open(file= "./model/training_dataset/True_test.csv", mode= "w") as test_file
):
    og_read = csv.reader(og)
    train_write = csv.writer(train_file)
    test_write = csv.writer(test_file)
    test = False

    header = next(og_read)
    test_write.writerow(header)
    train_write.writerow(header)

    for row in og_read:
        if test:
            test_write.writerow(row)
        else:
            train_write.writerow(row)
        test = not test

with (
        open(file= "./model/training_dataset/Fake.csv") as og,
        open(file= "./model/training_dataset/Fake_train.csv", mode= "w") as train_file,
        open(file= "./model/training_dataset/Fake_test.csv", mode= "w") as test_file
):
    og_read = csv.reader(og)
    train_write = csv.writer(train_file)
    test_write = csv.writer(test_file)
    test = False
    
    header = next(og_read)
    test_write.writerow(header)
    train_write.writerow(header)

    for row in og_read:
        if test:
            test_write.writerow(row)
        else:
            train_write.writerow(row)
        test = not test


